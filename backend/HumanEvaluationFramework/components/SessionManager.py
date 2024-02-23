from HumanEvaluationFramework.models import Session, SessionProgress
from datetime import datetime
from django.core import serializers
from HumanEvaluationFramework.components.enums import Result
from django.db.models import FloatField


class SessionManager:
    def __init__(self, session_id=None, name=None):
        if not session_id:
            self.name = name
            self.dataset = None
            self.session = None
        else:
            active_session = Session.objects.filter(id=session_id).first()
            self.name = active_session.name
            self.dataset = active_session.dataset
            self.session = active_session

    def register_new_session(self, dataset):
        self.dataset = dataset

        # delete old sessions
        Session.objects.filter(name=self.name, accuracy=None).delete()

        # create new ones
        session = Session(name=self.name, dataset=dataset, date=datetime.now())
        session.save()
        self.session = session

        return session.id

    def query_previous_session(self):
        return Session.objects.filter(name=self.name, accuracy=None).order_by('-date').first() is not None

    def set_previous_session(self):
        previous = Session.objects.filter(name=self.name, accuracy=None).order_by('-date').first()
        if previous:
            self.session = previous
            self.dataset = self.session.dataset
        else:
            raise ValueError(f'There are no previous sessions for {self.name}, yet it was queried.')

    def get_evaluated_count(self):
        return len(list(SessionProgress.objects.filter(session=self.session).exclude(result=-1)))

    def get_remaining_samples(self):
        return list(SessionProgress.objects.filter(session=self.session, result=-1).values('file', 'ground_truth'))

    def start_progress(self, samples):
        for sample in samples:
            entry = SessionProgress(session=self.session, file=sample['filename'], ground_truth=sample['ground_truth'], result=-1)
            entry.save()

    def enter_choice(self, filename, result, difficulty, time_taken, player_position, playcount, audio_length):
        sample = SessionProgress.objects.filter(session=self.session, file=filename).first()
        if sample:
            sample.result = result
            sample.difficulty = difficulty
            sample.time_taken = time_taken
            sample.audio_position = player_position
            sample.play_count = playcount
            sample.audio_length = audio_length
            sample.save()
        else:
            raise ValueError(f"Could not enter choice for {filename}, because it does not exist in the database.")

    def finalize_session(self):
        good_guesses = 0
        all_time_taken = 0
        entries = SessionProgress.objects.filter(session=self.session)
        for entry in entries:
            if entry.result == entry.ground_truth:
                good_guesses += 1
            all_time_taken += entry.time_taken if entry.time_taken is not None else 10

        accuracy = good_guesses / len(entries)
        session = self.session
        session.accuracy = accuracy
        session.time_taken = all_time_taken
        session.save()

        json_data = serializers.serialize('json', entries)
        with open(f'results/{self.name}_{self.dataset}_{self.session.id}.json', 'w') as output:
            output.write(json_data)

        entries.delete()

        return (int)((accuracy*100)//1), all_time_taken//1


import os
import random

from HumanEvaluationFramework.models import QueuedFiles, MediaState
from HumanEvaluationFramework.components.enums import Result


class MediaService:
    def __init__(self, state_id=None):
        self.data_dir = 'media/data'
        self.true_data = 'media/human'
        self.queue = []
        if not state_id:
            self.current_dataset = None
            self.current_sample = None
            self.state = None
            self.df = self.search_datasets()
        else:
            state = MediaState.objects.filter(id=state_id).first()
            self.current_dataset = state.current_dataset
            self.current_sample = state.current_sample
            self.state = state

            queue = QueuedFiles.objects.filter(state=state)
            for qf in queue:
                self.queue.append({'filename': qf.file, 'ground_truth': qf.ground_truth})

    def save(self):
        if self.state:
            self.state.current_sample = self.current_sample
            self.state.current_dataset = self.current_dataset
            self.state.save()
        else:
            state = MediaState(current_dataset=self.current_dataset, current_sample=self.current_sample)
            state.save()
            self.state = state
        
        QueuedFiles.objects.filter(state=self.state).delete()
        for file in self.queue[::-1]:
            qf = QueuedFiles(file=file["filename"] if "filename" in file else file["file"], ground_truth=file["ground_truth"], state=self.state)
            qf.save()

    def search_datasets(self):
        return [name for name in os.listdir(self.data_dir) if os.path.isdir(os.path.join(self.data_dir, name))]

    def get_datasets(self):
        return self.df

    def select_dataset(self, dataset, sample_size):
        supported_formats = ['mp3', 'wav', 'ogg']
        if dataset not in self.df:
            raise ValueError('Selected dataset is not an existing subfolder')

        self.current_dataset = dataset
        generated_path = os.path.join(self.data_dir, dataset)
        generated_files = [name for name in os.listdir(generated_path) if (os.path.isfile(os.path.join(generated_path, name)) and
                                                                           name.split('.')[-1] in supported_formats)]
        number_of_samples = min(sample_size, len(generated_files))
        generated_files = random.sample(generated_files, number_of_samples)

        human_path = self.true_data
        human_files = [name for name in os.listdir(human_path) if (os.path.isfile(os.path.join(human_path, name))and
                                                                           name.split('.')[-1] in supported_formats)]
        human_files = random.sample(human_files, number_of_samples)

        collection = []
        for f in human_files:
            collection.append({'filename': f, 'ground_truth': 1})
        for f in generated_files:
            collection.append({'filename': f, 'ground_truth': 2})

        random.shuffle(collection)
        self.queue = collection

        return collection

    def load_dataset(self, dataset, collection):
        self.current_dataset = dataset
        random.shuffle(collection)
        self.queue = collection

    def next_sample(self):
        prev_sample, next_sample, full_path = None, None, None
        empty = (len(self.queue) == 0)
        if self.current_sample is not None:
            prev_sample = self.current_sample
        if not empty:
            next_sample = self.queue.pop()
            if next_sample['ground_truth'] == 1:
                full_path = os.path.join(self.true_data, next_sample['filename'] if 'filename' in next_sample else next_sample['file'])
            else:
                full_path = os.path.join(self.data_dir, self.current_dataset, next_sample['filename'] if 'filename' in next_sample else next_sample['file'])

            full_path = full_path[len('/media'):]
            self.current_sample = next_sample['filename'] if 'filename' in next_sample else next_sample['file']


        return empty, prev_sample, full_path





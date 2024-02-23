# Human Evaluation Framework
## Scope of the project  
During an internship with TC&C Ltd., this project was developed with the aim of creating an internal tool to benchmark the performance and a level of deception of state-of-the-art deepfake voice generators. The primary aspiration of the framework was to assess the company's deepfake voice detection AI model (Carin Deepfake Guard) in comparison to human recognition capabilities.
I also took a major role in research and development of Carin Deepfake Guard AI model during that very same internship.

## Functionality
Last updated on [2023. 08. 24.]
This is a Django (4.2.4) + Vue.JS (3.3.4) based web application.
Its core functionality entails the following:
- listing the predefined generated and human dataset
- randomly sampling from them with a user defined ratio
- shuffling them
- and queining them up into a test set.

Users (identified by their name) can create or countinue new sessions. During a session a user can evaluate a given testset, by deciding whether they are authentic or synthetised samples and by giving a rating on the difficulty of this decision. Users are only allowed to listen each data sample twice. The entire progress is stored in a SQLite3 database with detailed metadata, such as: the datasource, the current file, the ground truth label, the user's decision, the time it took to make that decision, and the user selected difficulty of this decision. Per sample session storage allows the users the leave their progress anytime and pick up later on. During Upon completition, the user is presented with the achieved accuracy, and their progress is stored in a json file in the `backend/results` folder. The webapp is designed to track the time and additional metrics until completition.

## Featured technical elements
Required skills for the project: [Backend development]: Python, Django, databases, [Frontend development]: JavaScript, Vue.JS, HTML, CSS, web design, Photoshop. 
The web application demonstrates a sophisticated array of functionalities, encompassing intricate session management, robust database and media storage mechanisms, seamless integration of industry-standard web frameworks, and adept utilization of diverse third-party libraries. The meticulous architectural design laid the foundation for its development, ensuring a flawless and immersive user experience.

## How to run
### Requirements
- nodejs (16+)
- python (3.8+)

To set up the work environment issue the following commands:
```
cd frontend
npm install
pip install django
```

### Media storage
The media should be stored separately according to their datasource. Human samples under: `backend\media\human`, synthetised samples under: `backend\media\data` under their own folder (named accordingly the datasource)

### API
Application: localhost:8000
Results page: localhost:8000/results

The webapp also provides a `results` endpoint where all the results are shown by the users in a tabular form.

### Development mode
**Backend**:
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**Frontend**:
- in `frontend\src\axios.js` configure the `BASE_URL` according to the backend's url:port
- `npm run serve`

### Deployment mode
Commands are to be issued from their respective directories, assuming you have already made migrations to the backend if changes were applied, and configured the `BASE_URL`
**Frontend**: `npm run build`
**Backend**: `python manage.py runserver 0.0.0.0:8000`

(The `npm run build` command automatically copies the generated static web files (dist directory) to the `backend/frontend` folder, so make sure it exits before running the code. The Django server then will automatically host the static pages.)

### Maintenance
If the application is already deployed and it is in use, swap the `vue_app` endpoint from index.html to maintenance.html in the views.py file, to show to appropriate message for the user, so they won't use the application in a faulty stage, which otherwise would mess up the measurements. You can set the counter in the maintenance.html.

## Licensing

This project is licensed under the TC&C Ltd. Proprietary License. I have been granted permission to view and use the source code solely for non-commercial (personal portfolio demonstration) purposes. Modification, distribution, or reproduction of the source code in any form is strictly prohibited without explicit written consent from TC&C Ltd. The source code provided here represents a simplified model and does not accurately reflect the full capabilities of the company's products. https://www.tcandc.com

## Authorship
The project was developed by Balázs Hain including the design, graphics, and implementation of the web application (frontend & backend) with the collaboration of Csaba Juhasz (csaba.juhaszjr@tcandc.com).


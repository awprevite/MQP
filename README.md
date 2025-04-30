# Worcester, MA Cool Route App
This is a Major Qualifying Project (MQP) For WPI.  
The app uses Next and React for the front-end and flask and arcpy for the back-end.  
Provides cool and direct routes between two user provided points at a given time.  Cool routes factor in shade and air temperature in addition to distance.

## To set up and run the project follow these steps
1. Clone the repository  
`git clone https://github.com/awprevite/MQP.git`

### Front-end
The front-end can be viewed and interacted with, but the route calculation feature will not be accessible unless the back-end server is running.  
It can also be accessed [here](https://cool-routes.vercel.app).  

2. Navigate to the front-end folder  
`cd MQP/front-end/leaflet-app`   
3. Install dependencies  
`npm install`  
4. Run the development server  
`npm run dev`

### Back-end
The back-end cannot be run on others machines due to missing geodatabase and invalid paths.  

5. Navigate to the back-end folder  
`cd MQP/back-end`  
6. Run the python file  
`python server.py`  
7. Run the windows script. Can be done by double clicking in file explorer

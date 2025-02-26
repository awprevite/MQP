# Worcester Cool Route App
This project is for our Major Qualifying Project (MQP). In order to run the entire project a valid ArcGIS lisense is required, however the front-end can be interacted with without this.
The app uses React for the front-end and python and arcpy for the back-end. 

The data used comes from ... and is ...

The app will accept inputs from the user in the menu on the left of the screen including  
1. Origin and destination coordinates that can be updated by placing markers on the map  
2. Time by adjusting the input  
3. ...  

Once the user requests to calculate the route, a route from the origin to the destination will be generated and displayed  

## To set up and run the project follow these steps
1. Clone the repository 

### Front-end
2. Navigate to the front-end folder  
`cd front-end`  
3. Install dependencies  
`npm install`
4. Run the development server  
`npm start`

### Back-end
5. Clone the argis python environment from ArcGIS Pro  
6. Activate that environment  
7 Navigate to the back-end folder  
`cd ../back-end`  
8. Run the flask server  
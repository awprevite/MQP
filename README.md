# Worcester, MA Cool Route App
This project is for our Major Qualifying Project (MQP).
The app uses Next and React for the front-end and python and arcpy for the back-end. 

The data used comes from ... and includes a sidewalk network dataset of worcester and route layers for each hour of sunlight in the summer (6 am to 8 pm) generated with heat and shade maps.

The app will accept inputs from the user in the menu on the left of the screen including  
1. Origin and destination coordinates that can be updated by placing markers on the map  
2. Time by adjusting the input  
3. ...  

Once the user requests to calculate the route, the most direct route (blue) and the cool route (green) from the origin to the destination will be generated and displayed  

## To set up and run the project follow these steps
1. Clone the repository  
`git clone https://github.com/awprevite/MQP.git`

### Front-end
2. Navigate to the front-end folder  
`cd MQP/front-end`  
3. Install dependencies  
`npm install`
4. Run the development server  
`npm run dev`

### Back-end
The back-end cannot be run on others machines due to missing datasets and invalid paths
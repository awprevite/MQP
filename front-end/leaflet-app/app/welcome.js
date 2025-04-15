'use client';

const Welcome = ({setWelcomeOpen}) => {


  return (
    <>
      <div className='welcome-modal-overlay' onClick={() => {setWelcomeOpen(false)}}></div>
      <div className="welcome">
        <div className="welcome-content">
          <h1>Welcome to Cool Routes</h1>

          <p>
            This Cool Routes navigation tool is designed to enhance pedestrian climate resilience and help mitigate the impacts of the urban heat island effect. By visualizing thermally comfortable and shaded routes, the app guides users to safer, more enjoyable paths through the city.
          </p>

          <h2>User Guide</h2>
          <p>
            Click on the map to set your journey’s start and end points. Markers can be moved by clicking new locations on the map. You may also search for a specific address using the search bars. Select a time of day and press "Go" to see the direct route and the cool route between your selected points or addresses.
          </p>
          <p>
            You may toggle light and dark mode with the moon button, find your current location with the arrow button, toggle the visibility of the routes with the checkmark boxes, and toggle which point is being set when clicking the map with the start and end buttons.
          </p>
          <p>
            <span className="blue">Blue</span> corresponds to the cool route and start point.
          </p>
          <p>
            <span className="red">Red</span> corresponds to the direct route and end point.
          </p>
          <p>
            Press the small bar beneath the top menu to hide the menu, then press it again to reveal it.
          </p>

          <h2>Disclaimer</h2>
          <p>
            This tool is intended for informational and educational purposes only. While every effort has been made to ensure the accuracy and reliability of the data, sourced from the Global Lab at WPI, OpenStreetMap, ShadeMap, and MassGIS, the City of Worcester and project contributors cannot guarantee the complete accuracy or currency of the content. Users are encouraged to exercise discretion and take necessary precautions, particularly during extreme weather conditions.
          </p>
        </div>
        <button className='welcome-button' onClick={() => {setWelcomeOpen(false)}}>close</button>
      </div>
    </>
  );
}


export default Welcome;
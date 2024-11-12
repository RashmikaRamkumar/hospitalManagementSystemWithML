import React from "react";

const Biography = ({imageUrl}) => {
  return (
    <>
      <div className="container biography">
        <div className="banner">
          <img src={imageUrl} alt="whoweare" />
        </div>
        <div className="banner">
          <p>Biography</p>
          <h3>Who We Are</h3>
          <p>
          Welcome to HealthTrack, a comprehensive healthcare management system designed to streamline patient care and enhance communication between patients, doctors, and admins. Our platform provides seamless access to essential healthcare services, allowing patients to book appointments, view medical records, and submit feedback with ease. Doctors can utilize predictive tools and access patient data to provide enhanced care, while admins have full control over managing appointments, adding healthcare professionals, and ensuring smooth operations.

At HealthTrack, our goal is to create a user-friendly, efficient system that prioritizes patient care and improves healthcare workflows. We are committed to delivering a seamless experience that connects all parties, empowering patients to take control of their health and providing doctors and administrators the tools they need for effective healthcare management.
          </p>
         </div>
      </div>
    </>
  );
};

export default Biography;

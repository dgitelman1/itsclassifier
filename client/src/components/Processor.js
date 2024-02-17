import React, { useState } from "react";
import axios from "axios";
import Output from "./Output";

const Processor = ({ isDev }) => {
  const [originalTicket, setTicket] = useState("");
  const [loading, setLoading] = useState(false);
  const [outputData, setOutputData] = useState("");
  var prediction = "";

  var baseQuery = "";
  if (isDev) {
    baseQuery = "http://localhost:8080";
  } else {
    baseQuery = "https://kona.ucsd.edu/python";
  }
  const predictQuery = "/predict";

  const onSubmit = (e) => {
    e.preventDefault();

    if (!originalTicket) {
      alert("Please provide a ticket!");
      return;
    }

    predict(originalTicket);

    setTicket("");
  };

  const predict = async (originalTicket) => {
    try {
      var ticket = originalTicket.toString(); 

      setLoading(true);
      try {
          console.log("Awaiting Flask API...");
          const response = await axios.post('http://localhost:8080/predict', { ticket });
          prediction = response.data;
          console.log("Prediction: ", prediction);
      } catch (err) {
          console.error(err);
      }
      setLoading(false);

      console.log("Setting output data to ", prediction);
      setOutputData(prediction);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      {!loading && (
        <>
          <div
            style={{ display: "flex", flexDirection: "column" }}
            className="bubble"
            id="originalEmailInput"
          >
            <h3>Original Email</h3>
            <form className="ui form">
              <textarea
                id="original_email"
                type="text"
                value={originalTicket}
                onChange={(e) => setTicket(e.target.value)}
              />
            </form>

            <div style={{ float: "right" }}>
              <button className="ui button teal" onClick={onSubmit} id="1">
                Parse Ticket
              </button>
            </div>
          </div>

          <div className="bubble" id="parsingResultOutput">
            <Output isDev={isDev} outputData={outputData} />
          </div>
        </>
      )}
      {loading && (
        <>
          <div
            style={{ display: "flex", flexDirection: "column" }}
            className="bubble"
            id="originalEmailInput"
          >
            <h3>Classifier is loading...</h3>
            <div className="spinner-container">
              <div className="loading-spinner"></div>
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default Processor;
import React from "react";
import "./App.css";
import Section1 from "./components/Section1";

function App() {
  React.useEffect(() => { document.title = 'Exported Page'; }, []);
  return (
    <div className="App" data-page-type="sp">
      <Section1 />
    </div>
  );
}

export default App;
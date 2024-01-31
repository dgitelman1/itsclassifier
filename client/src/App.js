import './App.css';
import Processor from "./components/Processor";


function App() {
  const isDev = false;

  return (
    <div className="App">
      <Processor isDev={isDev}/>
    </div>
  );
}

export default App;

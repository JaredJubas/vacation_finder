import './Homepage.css';
import Navbar from '../Navbar/Navbar';

const HomePage = () => {
  return (
    <div className="home-page-container">
      <Navbar />
      <div className="home-container">
        <header className="home-header">
          <div className="header-container">
            <h1 className="title">Vacation Finder</h1>
            <p className="subtitle">Vacation finder tool</p>
            <div className="vacation-finder-button-container">
              <a className="vacation-finder-button" href="/vacationFinder">
                Get started!
              </a>
            </div>
          </div>
        </header>
      </div>
    </div>
  );
};

export default HomePage;

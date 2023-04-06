import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <li>
          <a href="/" className="title">
            Home
          </a>
        </li>
        <li>
          <a href="/vacationFinder">Vacation Finder</a>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

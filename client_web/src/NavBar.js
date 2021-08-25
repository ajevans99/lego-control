import { Navbar, Container } from 'react-bootstrap';

function NavBar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="#home">LEGO Control</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default NavBar;

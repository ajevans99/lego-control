import { Container, Row, Col } from 'react-bootstrap';
import './App.css';
import NavBar from './NavBar';
import AllLights from './AllLights';
import ControlPointStatus from './ControlPointStatus';

function App() {
  return (
    <>
      <NavBar />
      <Container className="standard-container gap-2">
        <Row className="justify-content-center">
          <Col>
            <AllLights />
          </Col>

          <Col>
            <ControlPointStatus />
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default App;

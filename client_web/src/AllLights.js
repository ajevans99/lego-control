import { gql, useMutation } from '@apollo/client';
import React from 'react';
import { Form, Button, Card } from 'react-bootstrap';

const ALL_LIGHTS_BRIGHTNESS_MUTATION = gql`
mutation AllLightsBrightnessMutation($brightness: Int!) {
    allLightsBrightnessMutation(brightness: $brightness) {
      brightness
      lightStrips {
        name
        id
      }
    }
  }
`

function AllLights() {
    let range;
    const [changeBrightness, { error, data }] = useMutation(ALL_LIGHTS_BRIGHTNESS_MUTATION);

    if (error) return `Error! ${error.message}`;

    const brightness = data !== undefined ? data.allLightsBrightnessMutation.brightness : 50;

    return (
        <Card className="h-100">
            <Card.Body>
            <Card.Title>All Lights</Card.Title>
            
            <Form>
                <div className="on-off-buttons d-grid gap-2">
                <Button variant="primary" size="lg" onClick={ e => {
                    e.preventDefault();
                    changeBrightness({ variables: { brightness: 100 }});
                }}>On</Button>
                <Button variant="secondary" size="lg" onClick={ e => {
                    e.preventDefault();
                    changeBrightness({ variables: { brightness: 0 }});
                }}>Off</Button>
                </div>
            
                <Form.Label>Brightness</Form.Label>
                <Form.Range ref={node => { range = node; }} onChange={ e => {
                    changeBrightness({ variables: { brightness: e.target.value }});
                }} value={brightness}/>
            </Form>
            </Card.Body>
        </Card>
    );
}

export default AllLights;
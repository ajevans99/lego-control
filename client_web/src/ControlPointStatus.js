import { gql, useQuery } from '@apollo/client';
import React from 'react';
import { Card, Table } from 'react-bootstrap';

const CONTROL_POINT_STATUS_QUERY = gql`
  query ControlPointStatusQuery {
    allControlPoints {
      edges {
        node {
          name
          online
        }
      }
    }
  }
`

function ControlPointStatus() {
    const { loading, error, data } = useQuery(CONTROL_POINT_STATUS_QUERY);

    if (loading) return 'Loading...';
    if (error) return `Error! ${error.message}`;

    const offlineNodes = data.allControlPoints.edges.filter(({ node }) => !node.online);
    const message = offlineNodes.length === 0 ? "All Raspberry Pi's are responsing" : "Some Raspberry Pi's are not responding";

    return (
        <Card className="h-100">
            <Card.Body>
            <Card.Title>Control Point Status</Card.Title>
            <Card.Subtitle className="mb-2 text-muted">{ message }</Card.Subtitle>
            <Table striped bordered hover className="control-table">
                <thead>
                <tr>
                    <th>Name</th>
                    <th>Status</th>
                </tr>
                </thead>
                <tbody>
                    {data.allControlPoints.edges.map( ({ node }, idx) => {
                        return <tr key={idx}>
                            <td>{node.name}</td>
                            <td>
                            <div className="led-box">
                                <div className={`led-${node.online ? 'green' : 'yellow'}`}></div>
                            </div>
                            </td>
                        </tr> 
                    })}
                </tbody>
            </Table>
            </Card.Body>
        </Card>
    );
}

export default ControlPointStatus;

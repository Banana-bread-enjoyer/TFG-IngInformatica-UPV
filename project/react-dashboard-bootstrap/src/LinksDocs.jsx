import React, { useState, useEffect } from "react";
import Table from "react-bootstrap/Table";

const LinksDocs = ({ licitacion }) => {
  const [groupedLinks, setGroupedLinks] = useState({});

  const groupLinksByType = (links) => {
    return links.reduce((acc, link) => {
      if (!acc[link.type_link.texto_tipo_link]) {
        acc[link.type_link.texto_tipo_link] = [];
      }
      acc[link.type_link.texto_tipo_link].push(link);
      return acc;
    }, {});
  };

  useEffect(() => {
    fetch(`http://localhost:8000/api/links`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const foundLinks = data.filter(
          (link) => link.id_licitacion == licitacion
        );
        console.log(groupLinksByType(foundLinks));
        setGroupedLinks(groupLinksByType(foundLinks));
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [licitacion]);

  return (
    <div className="container mt-3">
      <h3>Listado Links</h3>
      <Table striped bordered hover>
        <tbody>
          {Object.keys(groupedLinks).map((type) => (
            <tr>
              <td key={type}>{type}</td>
              <td key={type}>
                <ul>
                  {groupedLinks[type].map((link) => (
                    <li key={link.id_link}>
                      <a href={link.link}>{link.link}</a>
                    </li>
                  ))}
                </ul>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default LinksDocs;

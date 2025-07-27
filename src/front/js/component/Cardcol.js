import React from "react";

export const Cardcol = () => {
  return (
    <div className="box">
      <div className="category-badge bg-warning text-dark">Colmenas</div>
      <img
        src="https://i.blogs.es/718339/650_1000_flow-hive-front/650_1200.jpg"
        alt="Colmena moderna"
      />
      <div className="overlay">
        <h3>COLMENAS</h3>
        <p>
          Colmenas diseñadas para optimizar la producción de miel y facilitar su
          extracción. Resistentes, funcionales y adaptadas a todo tipo de apicultores.
        </p>
        <a href="#">Ver Categorías</a>
      </div>
    </div>
  );
};

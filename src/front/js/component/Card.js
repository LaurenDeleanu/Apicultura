import React from "react";

export const Card = () => {
  return (
    <div className="box">
      <div className="category-badge bg-warning text-dark">Humeadores</div>
      <img
        src="https://i0.wp.com/apicolaromero.wordpress.com/wp-content/uploads/2016/07/ahumador-vulkan-2.jpg?w=296&h=395&ssl=1"
        alt="Humeador"
      />
      <div className="overlay">
        <h3>HUMEADORES</h3>
        <p>Ideal para el manejo de colmenas sin estresar a las abejas. Fácil de usar y seguro.</p>
        <a href="categorias">Ver Categorias</a>
      </div>
    </div>
  );
};
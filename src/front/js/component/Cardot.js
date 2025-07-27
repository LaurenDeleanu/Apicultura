import React from "react";

export const Cardot = () => {
  return (
    <div className="box">
      <div className="category-badge bg-warning text-dark">Otras categorías</div>
      <img
        src="https://images.unsplash.com/photo-1587049352851-8d4e89133924?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt="Productos apícolas varios"
      />
      <div className="overlay">
        <h3>OTRAS CATEGORÍAS</h3>
        <p>
          Encuentra herramientas, accesorios y productos complementarios para facilitar tu trabajo en la apicultura.
        </p>
        <a href="#">Ver Categorías</a>
      </div>
    </div>
  );
};

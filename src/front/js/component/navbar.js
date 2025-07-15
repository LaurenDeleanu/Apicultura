import React from "react";
import Logo from "../../img/Logo.png";

export const Navbar = () => {
  const handleLogout = () => {
    alert("Sesión cerrada");
    // Aquí iría la lógica real de cerrar sesión, logout API, etc.
    const modalEl = document.getElementById("logoutModal");
    const modal = window.bootstrap.Modal.getInstance(modalEl);
    modal.hide();
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg" style={{ backgroundColor: "#ffcc00" }}>
        <div className="container-fluid">
          <a className="navbar-brand me-3" href="#">
            <img src={Logo} alt="APIculturaArias Logo" className="navbar-logo" />
          </a>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
            <ul className="navbar-nav mb-2 mb-lg-0">
              <li className="nav-item dropdown custom-dropdown">
                <a
                  className="nav-link text-dark fw-bold fs-5 custom-hover"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Categorías
                </a>

                <ul className="dropdown-menu bg-dark">
                  <li><a className="dropdown-item" href="#">Humeadores</a></li>
                  <li><a className="dropdown-item" href="#">yks</a></li>
                  <li><hr className="dropdown-divider" /></li>
                  <li><a className="dropdown-item" href="#">Otros</a></li>
                </ul>
              </li>

              <form className="d-flex ms-3" role="search">
                <input className="form-control me-2" type="search" placeholder="Busqueda" aria-label="Search" />
                <button className="btn btn-outline-dark" type="submit">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-search" viewBox="0 0 16 16">
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
                  </svg>
                </button>
              </form>

              <li className="nav-item custom-user">
                <button
                  type="button"
                  className="btn nav-link text-dark ms-2 me-1 navbar-user"
                  data-bs-toggle="modal"
                  data-bs-target="#logoutModal"
                  aria-label="Cerrar sesión"
                  style={{ cursor: "pointer" }}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="27" height="27" fill="currentColor" className="bi bi-person-fill-lock" viewBox="0 0 16 16">
                    <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0m-9 8c0 1 1 1 1 1h5v-1a2 2 0 0 1 .01-.2 4.49 4.49 0 0 1 1.534-3.693Q8.844 9.002 8 9c-5 0-6 3-6 4m7 0a1 1 0 0 1 1-1v-1a2 2 0 1 1 4 0v1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1zm3-3a1 1 0 0 0-1 1v1h2v-1a1 1 0 0 0-1-1" />
                  </svg>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Modal cierre de sesión */}
      <div
  className="modal fade"
  id="logoutModal"
  tabIndex="-1"
  aria-labelledby="logoutModalLabel"
  aria-hidden="true"
>
  <div className="modal-dialog modal-dialog-centered">
	<div className="modal-content bg-dark text-light">

      <div className="modal-header border-0">
        <h5 className="modal-title" id="logoutModalLabel">Cerrar sesión</h5>
        <button
          type="button"
          className="btn-close btn-close-white"
          data-bs-dismiss="modal"
          aria-label="Cerrar"
        ></button>
      </div>
	  <hr className="custom-white-separator" />
      <div className="modal-body">
        ¿Seguro que quieres cerrar sesión?
      </div>
      <div className="modal-footer border-0">
        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
        <button type="button" className="btn btn-warning" onClick={handleLogout}>Aceptar</button>
      </div>
    </div>
  </div>
</div>
    </>
  );
};

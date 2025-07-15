import React, { useContext } from "react";
import { Context } from "../store/appContext";
import Logo from "../../img/Logo.png";
import Logobee from "../../img/logobee.png";
import "../../styles/home.css";

export const Sesion = () => {
 return (
    <section className="vh-100">
      <div className="container-fluid h-custom">
        <div className="row d-flex justify-content-center align-items-center h-100">
          <div className="col-md-9 col-lg-6 col-xl-5">
            <img src={Logobee} alt="APIculturaArias Logo" className="img-fluid invert-image mt-5 mb-5" />
          </div>

          <div className="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
            <form>

              <div className="divider d-flex align-items-center my-4">
                <img src={Logo} alt="APIculturaArias Logo" className="navbar-logo-sesion invert-image" />
              </div>

              <div className="form-outline mb-4">
                <input
                  type="text"
                  id="username"
                  className="form-control form-control-lg"
                  placeholder="Introduzca un usuario"
                />
                <label className="form-label" htmlFor="form3Example3">Usuario</label>
              </div>
              <div className="form-outline mb-3">
                <input
                  type="password"
                  id="form3Example4"
                  className="form-control form-control-lg"
                  placeholder="Introduzca su contraseña"
                />
                <label className="form-label" htmlFor="form3Example4">Contraseña</label>
              </div>
              <div className="text-center text-lg-start mt-4 ">
                <button type="button" className="btn btn-warning btn-lg " style={{ paddingLeft: "2.5rem", paddingRight: "2.5rem" }}>
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import { Card } from "../component/Card";
import { Cardcol } from "../component/Cardcol";
import { Cardtraj } from "../component/Cardtraj";
import "../../styles/home.css";

export const Categorias = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<div className="cartas">
			<Card />
			<Cardcol />
			<Cardtraj />
			</div>
		</div>
	);
};

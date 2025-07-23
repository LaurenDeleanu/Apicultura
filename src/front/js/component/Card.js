import React from "react";

export const Card = () => {
  return (
    <div className="container">
      <div className="column">
        <div className="post-module">
          <div className="thumbnail">
            <img src="https://i0.wp.com/apicolaromero.wordpress.com/wp-content/uploads/2016/07/ahumador-vulkan-2.jpg?w=296&h=395&ssl=1" />
          </div>
          <div className="post-content">
            <div className="category">Humeador</div>
            <h4 className="title">AHUMADOR DE GEORGE THE LAYENS</h4>
            <h2 className="sub_title">dcd</h2>
            <p className="description">cds</p>
            <div className="post-meta">
              <span className="timestamp"><i className="fa fa-clock-o"></i> dc</span>
              <span className="comments"><i className="fa fa-comments"></i></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
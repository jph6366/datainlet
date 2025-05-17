import React from "react";
import {createRoot} from "react-dom/client"
import { Map } from "react-map-gl/maplibre";
// import { Map } from "react-map-gl/mapbox";
// import DeckGL, { Layer, PickingInfo } from "deck.gl";
// import { _GeoArrowTextLayer } from "@geoarrow/deck.gl-layers";
// import * as arrow from "apache-arrow";
import MAP_STYLE from './map-style-basic-v8.json';


const INITIAL_VIEW_STATE = {
  latitude: 18.03403641639511,
  longitude: -64.91530172951025,
  zoom: 8,
  bearing: 0,
  pitch: 0,
};


const NAV_CONTROL_STYLE = {
  position: "absolute",
  top: 10,
  left: 10,
};

function Root() {

    return (
      <>
        <Map initialViewState={INITIAL_VIEW_STATE}
        mapStyle={MAP_STYLE}>
        </Map>
      </>
    )
}

export function renderToDom(container:any) {
  createRoot(container).render(<Root />);
}
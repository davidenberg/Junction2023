import Map from 'react-map-gl';
import DeckGL, { PathLayer } from 'deck.gl/typed';
import route1 from './route1.json';
import route2 from './route2.json';
import route3 from './route3.json';
import { useState } from 'react';

const INITIAL_VIEW_STATE = {
  latitude: 60.21,
  longitude: 24.78,
  zoom: 13,
  bearing: 0,
  pitch: 30
};

type LatLng = {
  latitude: number,
  longitude: number
}
type Route = {
  path: LatLng[],
  warnings: LatLng[][]
}

export default function App() {
  const [selectedRoute, setSelectedRoute] = useState('route0');
  const [warningsVisible, setWarningsVisible] = useState(false);
  const paths = [(route1 as Route).path, (route2 as Route).path, (route3 as Route).path];
  const warnings = [(route1 as Route).warnings, (route2 as Route).warnings, (route3 as Route).warnings];
  const layers = [
    paths.map((route, i) => new PathLayer({
      id: 'path-layer' + i,
      data: [route.map((e) => [e.longitude, e.latitude])],
      pickable: true,
      widthScale: 10,
      widthMinPixels: 2,
      getPath: d => d,
      getColor: () => [0, 0, 255],
      getWidth: () => 1,
      visible: selectedRoute === 'route' + i
    })),
    warnings.map((route, i) => new PathLayer({
      id: 'warnings-layer' + i,
      data: route.map((e) => e.map((i) => [i.longitude, i.latitude])),
      pickable: true,
      widthScale: 15,
      widthMinPixels: 2,
      getPath: d => d,
      getColor: () => [255, 0, 0],
      getWidth: () => 1,
      visible: selectedRoute === 'route' + i && warningsVisible
    }))
  ];

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      layers={layers}
    >
      <div style={{ position: 'absolute', width: '10%', backgroundColor: 'black', color: 'white' }}>
        <div>
          <input type="radio" id='participant1' name="layer" onChange={() => setSelectedRoute('route0')} defaultChecked />
          <label htmlFor="participant1">Participant 1</label>
        </div>
        <div>
          <input type="radio" id='participant2' name="layer" onChange={() => setSelectedRoute('route1')} />
          <label htmlFor="participant2">Participant 1 Round 2</label>
        </div>
        <div>
          <input type="radio" id='participant3' name="layer" onChange={() => setSelectedRoute('route2')} />
          <label htmlFor="participant3">Participant 3</label>
        </div>
        <br />
        <div>
          <input type="checkbox" id='warnings' defaultChecked onChange={() => setWarningsVisible(!warningsVisible)} />
          <label htmlFor="participant3">Warnings visible</label>
        </div>
      </div>
      <Map
        mapLib={import('mapbox-gl')}
        style={{ width: 600, height: 400 }}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        mapboxAccessToken='pk.eyJ1Ijoiam9oYW5uZXNwZWx0b2xhMiIsImEiOiJjbG91Mmxnb3kwZjYyMmtsOWxhMnRwbzFmIn0.yI81GPmuDaTjnbdhanni5g'
      />;
    </DeckGL >
  );
}

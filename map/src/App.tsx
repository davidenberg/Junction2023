import Map from 'react-map-gl';
import DeckGL, { PathLayer } from 'deck.gl/typed';
import route from './route1.json';

const INITIAL_VIEW_STATE = {
  latitude: 60.21,
  longitude: 24.78,
  zoom: 13,
  bearing: 0,
  pitch: 30
};

export default function App() {
  const layers = [
    new PathLayer({
      id: 'path-layer',
      data: [route.path.map((e) => [e.longitude, e.latitude])],
      pickable: true,
      widthScale: 10,
      widthMinPixels: 2,
      getPath: d => d,
      getColor: () => [0, 0, 255],
      getWidth: () => 1
    }),
    new PathLayer({
      id: 'warnings-layer',
      data: route.warnings.map((e) => e.map((i) => [i.longitude, i.latitude])),
      pickable: true,
      widthScale: 15,
      widthMinPixels: 2,
      getPath: d => d,
      getColor: () => [255, 0, 0],
      getWidth: () => 1
    })

  ];

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      layers={layers}
    >
      <Map
        mapLib={import('mapbox-gl')}
        style={{ width: 600, height: 400 }}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        mapboxAccessToken='pk.eyJ1Ijoiam9oYW5uZXNwZWx0b2xhMiIsImEiOiJjbG91Mmxnb3kwZjYyMmtsOWxhMnRwbzFmIn0.yI81GPmuDaTjnbdhanni5g'
      />;
    </DeckGL>
  );
}

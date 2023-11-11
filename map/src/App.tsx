import Map from 'react-map-gl';
import DeckGL, { HeatmapLayer, PathLayer } from 'deck.gl/typed';
import route0 from './route1.json';
import route1 from './route2.json';
import route2 from './route3.json';
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

type Routes = 'route0' | 'route1' | 'route2' | 'heatmap';

export default function App() {
  const [selectedLayer, setSelectedLayer] = useState<Routes>('route0');
  const [warningsVisible, setWarningsVisible] = useState(true);
  const paths = [(route0 as Route).path, (route1 as Route).path, (route2 as Route).path];
  const warnings = [(route0 as Route).warnings, (route1 as Route).warnings, (route2 as Route).warnings];
  const heatmapData = warnings.flat(2);
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
      visible: selectedLayer === 'route' + i
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
      visible: selectedLayer === 'route' + i && warningsVisible
    })),
    new HeatmapLayer({
      id: 'heatmapLayer',
      data: heatmapData,
      getPosition: (d) => [d.longitude, d.latitude],
      aggregation: 'SUM',
      visible: selectedLayer === 'heatmap'
    })
  ];

  const routes: { [key: string]: Route } = {
    route0: route0 as Route,
    route1: route1 as Route,
    route2: route2 as Route
  }

  function getDriverScore() {
    const route = routes[selectedLayer];
    const pathLength = route.path.length;
    const warningsLength = route.warnings.reduce((prev, curr) => prev + curr.length, 0);
    const score = (1 - warningsLength / pathLength) * 100;
    return <p style={{ fontSize: '5rem', marginTop: 0 }}>{score.toFixed(2)}<p style={{ fontSize: '2rem', margin: 0 }}>/100</p></p>
  }

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      layers={layers}
    >
      <div style={{
        position: 'absolute',
        right: 0,
        width: '10%',
        backgroundColor: 'rgba(0,0,0,0.6)',
        color: 'white',
        padding: '1rem',
        minWidth: '12em'
      }}>
        <div>
          <input type="radio" id='participant1' name="layer" onChange={() => setSelectedLayer('route0')} defaultChecked />
          <label htmlFor="participant1">Participant 1</label>
        </div>
        <div>
          <input type="radio" id='participant2' name="layer" onChange={() => setSelectedLayer('route1')} />
          <label htmlFor="participant2">Participant 1 Round 2</label>
        </div>
        <div>
          <input type="radio" id='participant3' name="layer" onChange={() => setSelectedLayer('route2')} />
          <label htmlFor="participant3">Participant 3</label>
        </div>
        <div>
          <input type="radio" id='heatmap' name="layer" onChange={() => setSelectedLayer('heatmap')} />
          <label htmlFor="heatmap">Heatmap</label>
        </div>
        <br />
        <div>
          <input type="checkbox" id='warnings' defaultChecked disabled={selectedLayer === 'heatmap'} onChange={() => setWarningsVisible(!warningsVisible)} />
          <label htmlFor="participant3">Warnings visible</label>
        </div>
      </div>
      {selectedLayer !== 'heatmap' && (
        <div style={{
          position: 'absolute',
          right: 0,
          top: '35%',
          width: '15%',
          height: '25%',
          backgroundColor: 'rgba(0,0,0,0.8)',
          color: 'white',
          padding: '0.5em',
          textAlign: 'center',
          minWidth: '13rem',
          minHeight: '16rem'
        }}>
          <h2>Driver Score</h2>
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'center' }}>
            {getDriverScore()}
          </div>
        </div>
      )}
      <Map
        mapLib={import('mapbox-gl')}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        mapboxAccessToken='pk.eyJ1Ijoiam9oYW5uZXNwZWx0b2xhMiIsImEiOiJjbG91Mmxnb3kwZjYyMmtsOWxhMnRwbzFmIn0.yI81GPmuDaTjnbdhanni5g'
      />;
    </DeckGL >
  );
}

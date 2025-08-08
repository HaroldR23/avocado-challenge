import { Provider } from 'react-redux';
import { store } from './store';
import Layout from './components/Layout/Layout';
import TaskList from './components/Tasks/TaskList';

function App() {
  return (
    <Provider store={store}>
      <Layout>
        <div>
          <TaskList />
        </div>
      </Layout>
    </Provider>
  );
}

export default App;

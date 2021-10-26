import React, { useState } from 'react';
import './App.css';

// styling
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css';

// app-switching
import { Redirect } from 'react-router';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import modules from './pages'; // All the parent knows is that it has modules ...
import Switch from 'react-bootstrap/Switch';

// data fetch
import { Footer } from 'components/footer';
import { NavHeader } from 'components/navHeader';
import { UserContextWrapper } from 'components/userContextWrapper';
import { QueryClientWrapper } from 'components/queryClientWrapper';

function AppRouter() {
    // state
    const [currentTab, setCurrentTab] = useState('BenchmarkSearch');

    return (
        <Router>
            <NavHeader setCurrentTab={setCurrentTab} />
            <div className="App">
                <div className="App-content my-3">
                    <Switch>
                        <Route exact path="/">
                            <Redirect to={modules.ResultSearchModule.path} />
                        </Route>
                        {modules.all.map((module) => (
                            <Route
                                path={module.path}
                                component={module.element}
                                key={module.name}
                            />
                        ))}
                    </Switch>
                </div>
            </div>
            <Footer setCurrentTab={setCurrentTab} />
        </Router>
    );
}

export default (
    <QueryClientWrapper>
        <UserContextWrapper>
            <AppRouter />
        </UserContextWrapper>
    </QueryClientWrapper>
);

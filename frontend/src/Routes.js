import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Today from './screens/Today'
import History from './screens/History'
import Header from './screens/Header'
import Log from './screens/Log'

export default () => (
  <Router>
    <Header />
    <Route path="/today" component={Today} />
    <Route path='/history/:id' component={Log}></Route>
    <Route path="/history" component={History} />
  </Router>
)
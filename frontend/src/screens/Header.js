import React from 'react';
import { Link } from "react-router-dom";
import Button from '@material-ui/core/Button'

function Header() {
  return (
    <div>
      <Link style={{textDecoration: 'none'}} to='/today'>
        <Button className='headerbutton'>
          <h1>Today</h1>
        </Button>
      </Link>
      <Link style={{textDecoration: 'none'}} to='/history'>
        <Button className='headerbutton'>
          <h1>History</h1>
        </Button>
      </Link>
    </div>
  )
}

export default Header;
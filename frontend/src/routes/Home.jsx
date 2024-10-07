import { useEffect, useState } from 'react'
import '../App.css'
import axios from 'axios'


import Nav from '../components/Nav'
import { Hero, Features } from "../sections";

function Home() {

  return (
    <main className='bg-[#fbfbfb]'>
      <Nav />
      <section>
        <Hero />
      </section>
      <section>
        <Features />
      </section>
    </main>
  )
}

export default Home

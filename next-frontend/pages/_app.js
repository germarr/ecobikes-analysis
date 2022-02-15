import Navbar from '../components/Navbar'
import '../styles/globals.css'

function MyApp({ Component, pageProps }) {
  return (
    <div className='bg-slate-800 min-h-screen'>
      <Navbar/>
      <Component {...pageProps} />
    </div>
  )
}

export default MyApp

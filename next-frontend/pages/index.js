import Head from 'next/head'
import Dropdown from '../components/Dropdown';

export default function Home() {

  return (
    <div>
      <Head>
        <title>Home</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* All Page Container */}
      <div className='mx-11'>
        {/* Top Banner */}
        <Dropdown url="./dashboard/map"/>
      </div>
    </div>
  )
}


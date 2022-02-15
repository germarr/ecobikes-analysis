import React, { useState } from 'react';
import Link from 'next/link';

export default function Dropdown({url}) {
    const meses = [{name:"Seleccionar",num:0},{name:"Ene",num:1},{name:"Feb",num:2},{name:"Mar",num:3},{name:"Abr",num:4},{name:"May",num:5},{name:"Jun",num:6},{name:"Jul",num:7},{name:"Ago",num:8},{name:"Sep",num:9},{name:"Oct",num:10},{name:"Nov",num:11},{name:"Dic",num:12}]
    const anios = [{year:"Seleccionar"},{year:2021},{year:2020},{year:2019}]

    const [month, setMonth] = useState(4);
    const [anio, setAnio] = useState(2021);
  
    function handleChange(event){
        setAnio(event.target.value)
    }  

    function handleChangeII(event){
        setMonth(event.target.value)
    }

    return(
        <div className='mb-5 bg-slate-500 border-2 rounded-tl-lg rounded-br-lg'>
            <div className=' flex flex-col md:flex-row py-2 items-center md:justify-center'>
                <div className='md:py-0 md:pr-6 pb-3 md:pb-0'>
                    <h1 className="text-center pl:0  text-2xl md:text-4xl font-bold text-white"> Dashboard 📊</h1>
                </div>
                <div className='flex flex-col md:flex-row divide-y-2 md:divide-y-0 md:divide-x-2 divide-slate-300 md:py-5'> 
                    <div className='md:pt-12 pt-0 pl-32 md:pl-1'></div>
                    <div className='md:pb-12 pb-0 pr-32 md:pr-1'></div>
                </div>  
                <div className='flex flex-row md:flex-row pt-2 pb-3 md:pt-0 md:pb-0'> 
                    <div className='flex flex-col px-6 space-y-1'>
                    <p className='font-semibold text-white'>Año</p>
                    <div>
                        <select onChange={handleChange} id="estados" className="w-24 h-5 pl-3 pr-6 text-xs placeholder-gray-600 border  appearance-none focus:shadow-outline shadow-sm" placeholder="Regular input">
                            {anios.map((e)=>{
                                return(
                            <option className='text-center' key={`${e.year}`} value={`${e.year}`}>{e.year}</option> 
                                )
                            })}
                        </select>
                    </div>
                    </div>
                    <div className='flex flex-col px-6 space-y-1'>
                    <p className='font-semibold text-white'>Mes</p>
                    <div>
                        <select onChange={handleChangeII} id="estados" className="w-24 h-5 pl-3 pr-6 text-xs placeholder-gray-600 border  appearance-none focus:shadow-outline shadow-sm" placeholder="Regular input">
                            {meses.map((e)=>{
                                return(
                            <option className='text-center' key={`${e.num}`} value={`${e.num}`}>{e.name}</option> 
                                )
                            })}
                        </select>
                    </div>
                    </div>
                </div>
            </div>
            <div className='flex items-center justify-center pb-5'>
                <h2 className='font-base text-white text-lg text-center'>Para conocer las métricas más relevantes de <span className='font-semibold'>Ecobici</span>, solo selecciona un mes/año y da click en el 
                    botón "Buscar".
                </h2>
            </div>
            <div className='flex'>
                <Link href={`${url}?mes=${month}&anio=${anio}`}>
                    <button id="searchButton" type="button" className='bg-slate-300 hover:bg-slate-200 w-full text-slate-800'>
                    <div className="flex items-center justify-center space-x-2">
                        <div>
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 md:w-6 md:h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg> 
                        </div>
                        <div className='font-bold uppercase py-2 text-base'>BUSCAR</div>
                    </div>
                    </button>
                </Link>
            </div>
      </div>
  );
}



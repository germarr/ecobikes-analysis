import React from 'react';

export default function TopCards({titulo, valor, mom, yoy}) {
    let momI = parseInt(mom)
    let yoyI = parseInt(yoy)
    let mom_color;
    let yoy_color;

    if(momI >= 0){
        mom_color = "bg-green-300 rounded-tr-md rounded-bl-md text-green-800 font-bold px-3"
    }else{
        mom_color = "bg-red-300 rounded-tr-md rounded-bl-md text-red-800 font-bold px-3"
    }

    if(yoyI >= 0){
        yoy_color = "bg-green-300 rounded-tr-md rounded-bl-md text-green-800 font-bold px-3"
    }else{
        yoy_color = "bg-red-300 rounded-tr-md rounded-bl-md text-red-800 font-bold px-3"
    }

  return (
    <div>
        <div className='border-2 border-x-white rounded-t-md bg-slate-600 shadow-white shadow-sm'>
            <div className='p-1 flex flex-col space-y-1'>
                <h2 className='font-normal text-white text-xs md:text-base text-center'>{titulo}</h2>
                <div className='divide-y divide-slate-300 px-5'>
                    <div className='pb-1'></div>
                    <div className='pt-1'></div>
                </div>
                <div className='flex flex-col md:flex-row items-center justify-between px-0 md:px-5 pb-2'>
                    <div className='flex'>
                    <h2 className='font-semibold text-white text-base md:text-lg'>{valor}</h2>
                </div>
                <div className='pt-1 md:pt-0 flex space-x-1 md:space-x-3'>                
                    <div className='flex-col text-xs text-center space-y-1'>
                        <p className='text-white font-light'>MoM</p>
                        <p className={mom_color}>{momI}%</p>
                    </div>                
                    <div className='flex-col text-xs text-center space-y-1'>
                      <p className='text-white font-light'>YoY</p>
                      <p className={yoy_color}>{yoyI}%</p>
                    </div>
                </div>
              </div>
            </div>
          </div>
    </div>
  );
}

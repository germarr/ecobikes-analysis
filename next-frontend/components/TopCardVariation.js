import React from 'react';

export default function TopCardVariation({titulo, valor, mom}) {

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
                    <h2 className='font-semibold text-white text-xs text-center md:text-left md:text-sm'>{valor}</h2>
                </div>
                <div className='pt-1 md:pt-0 space-x-1 md:space-x-3'>                
                    <div className='flex flex-row md:flex-col text-xs md:text-center space-x-1 md:space-x-0 md:space-y-1'>
                        <p className='text-white font-semibold'>Viajes</p>
                        <p className="text-white font-normal">{mom}</p>
                    </div>  
                </div>
              </div>
            </div>
          </div>
    </div>
  );
}

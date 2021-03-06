import Head from 'next/head'
import Dropdown from '../../components/Dropdown';
import TopCards from '../../components/TopCards';
import TopCardVariation from '../../components/TopCardVariation';
import { supabase } from '../../utils/supabase';


export default function Month({ganancias, kilometros, viajes_totales, tiempo_total, estacion, titulo}) {

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
        <Dropdown url="/dashboard/map"/>
        {/* Title of the page */}
        <div className='flex items-center'>
          <h2 className='text-white text-2xl font-semibold underline text-center md:text-left'>Métricas de {titulo.nombre_mes} del {titulo.anio_mes}.</h2>
        </div>
        {/* Top Cards */}
        <div className='grid grid-cols-2 md:grid-cols-5 gap-3 mt-5'>
          <TopCards titulo="Viajes Totales 🚦" valor={`${viajes_totales["mes"]} viajes`} mom={viajes_totales["mes_pasado"]} yoy={viajes_totales["anio_pasado"]}/>
          <TopCards titulo="Km's del mes 🌎" valor={`${kilometros["mes"]} kms`} mom={kilometros["mes_pasado"]} yoy={kilometros["anio_pasado"]}/>
          <TopCards titulo="Tiempo Recorrido ⏰" valor={`${tiempo_total["mes"]} horas`} mom={tiempo_total["mes_pasado"]} yoy={tiempo_total["anio_pasado"]}/>
          <TopCards titulo="Ingresos del Mes 💸" valor={`$ ${ganancias["mes"]}`} mom={ganancias["mes_pasado"]} yoy={ganancias["anio_pasado"]}/>
          <TopCardVariation titulo="Estación mas popular 🏁" valor={estacion["nombre"]} mom={`${estacion["viajes"]}`}/>
        </div>
      </div>
    </div>
  )
}

export const getServerSideProps = async (context)=>{

  const anio_var = parseInt(context.query.anio);
  const mes_var = parseInt(context.query.mes) + 11;
  
  const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
  
  let supa_callII = await supabase.from("ecobici_cards").select("*").lte("anio", anio_var).gte("anio", anio_var-1)

  const sup_data = supa_callII["data"]

  // Filtrar por los útltimos 2 años y generarles un id a cada mes. 
  function getMonthlyIds(){
    let months_dict = []
  
    for(let i = 0; i < sup_data.length; i++){
      months_dict.push({
        id:i,
        anio:sup_data[i].anio,
        mes_num:sup_data[i].Mes,
        mes_nombre:monthNames[sup_data[i].Mes-1],
        metrica:sup_data[i].viajes
      })
    }

    return months_dict
  }

  let months_dict = getMonthlyIds()

  // Función para crear las listas de datos que necesita la grafica.
  function getgraph(){
    let graph_list = []
  
    for(let j=0; j < months_dict.length; j++){
      if(months_dict[j].id <= mes_var && months_dict[j].id >= mes_var - 5){
        graph_list.push({
          mes:months_dict[j].mes_nombre,
          viajes:months_dict[j].metrica
          })
      }
    }

    let exportlistNames = []
    let exportlistValues = []

    for(let k=0; k < graph_list.length; k++){
      exportlistNames.push(graph_list[k].mes)
      exportlistValues.push(graph_list[k].viajes)
    }

    return [exportlistNames, exportlistValues]

  }

  const graphData = getgraph()

  // Obtener los datos de las tarjetas
  function datosDeTarjetas(){
    let m_dict = []

    if(mes_var-11 === 1){

      for(let m=0; m < sup_data.length; m++){
        
        if(sup_data[m].Mes === 1 || sup_data[m].Mes === 12){
          m_dict.push(sup_data[m])
        }
  
      }

    }else{   
      for(let m=0; m < sup_data.length; m++){
        
        if(sup_data[m].Mes === mes_var - 11 || sup_data[m].Mes === mes_var - 12){
          m_dict.push(sup_data[m])
        }
  
      }
    }
    
    return m_dict
  }

  //Datos para las tarjetas
  const m_dicc = datosDeTarjetas()
  const month_dict = m_dicc[3]
  let last_month_dict = m_dicc[2]
  let last_year_dict = m_dicc[1]
  
  function construirTarjetas(){

    const month_revenue = month_dict["ganancia_total"]
    let last_month_revenue = ((month_revenue - last_month_dict["ganancia_total"]) / last_month_dict["ganancia_total"]) * 100
    let last_year_revenue = ((month_revenue - last_year_dict["ganancia_total"]) / last_year_dict["ganancia_total"]) * 100
  
    const month_kms = month_dict["distancia_total"]
    let last_month_kms = ((month_kms - last_month_dict["distancia_total"]) / last_month_dict["distancia_total"]) * 100
    let last_year_kms = ((month_kms - last_year_dict["distancia_total"]) / last_year_dict["distancia_total"]) * 100
  
    const month_trips = month_dict["viajes"]
    let last_month_trips = ((month_trips - last_month_dict["viajes"]) / last_month_dict["viajes"]) * 100
    let last_year_trips = ((month_trips - last_year_dict["viajes"]) / last_year_dict["viajes"]) * 100
  
    const month_time = month_dict["tiempo_total"]
    let last_month_time = ((month_time - last_month_dict["tiempo_total"]) / last_month_dict["tiempo_total"]) * 100
    let last_year_time = ((month_time - last_year_dict["tiempo_total"]) / last_year_dict["tiempo_total"]) * 100

    return [last_month_revenue, last_year_revenue, last_month_kms, last_year_kms, last_month_trips, last_year_trips, last_month_time, last_year_time]
  }

  let [last_month_revenue, last_year_revenue, last_month_kms, last_year_kms, last_month_trips, last_year_trips, last_month_time, last_year_time] = construirTarjetas()
  
  return{
    props:{
        titulo:{
          nombre_mes:monthNames[parseInt(context.query.mes) - 1],
          anio_mes:anio_var
        },
        graficaOne:{
          nombres:graphData[0],
          valores:graphData[1]
        },
        ganancias:{
            mes:parseInt(month_dict["ganancia_total"]).toLocaleString(),
            mes_pasado: last_month_revenue,
            anio_pasado : last_year_revenue
        },
        kilometros:{
            mes:parseInt(month_dict["distancia_total"]).toLocaleString(),
            mes_pasado: last_month_kms,
            anio_pasado: last_year_kms
        },
        viajes_totales:{
            mes:month_dict["viajes"].toLocaleString(),
            mes_pasado: last_month_trips,
            anio_pasado: last_year_trips
        },
        tiempo_total:{
            mes:parseInt(month_dict["tiempo_total"]).toLocaleString(),
            mes_pasado: last_month_time,
            anio_pasado: last_year_time
        },
        estacion:{
            nombre:month_dict["name_retiro"],
            viajes:month_dict["viajes_iniciados"]
        }
    }
  }
}
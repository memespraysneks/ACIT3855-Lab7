import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://caleblab3855.eastus2.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        console.log(stats['num_items_created'])
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Items Created</th>
							<th>Items Traded</th>
						</tr>
						<tr>
							<td># IC: {stats['num_items_created']}</td>
							<td># IT: {stats['num_trades']}</td>
						</tr>
						<tr>
							<td colSpan="2">Max Strength: {stats['max_str']}</td>
						</tr>
						<tr>
							<td colSpan="2">Max Dexterity: {stats['max_dex']}</td>
						</tr>
						<tr>
							<td colSpan="2">Max Intelligence: {stats['max_int']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}

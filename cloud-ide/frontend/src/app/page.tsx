// "use client"
// import { useState, useEffect } from 'react';
// import axios from 'axios';
import HomepageForm from '@/components/homepage-form'

export default function Home() {

  // const [message, setMessage] = useState<string>('');

  // useEffect(() => {
  //     axios.get('http://localhost:4000/api/hello')
  //         .then(response => setMessage(response.data.message))
  //         .catch(error => console.error('Error fetching message:', error));
  // }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col row-start-2 justify-center items-center">
        {/* <div>
            <h1>Next.js + Express Example with TypeScript</h1>
        </div>
        <div>
            <p>{message || 'Loading...'}</p>
        </div> */}

        <HomepageForm />
      </main>
    </div>
  );
}

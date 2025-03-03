import Image from "next/image";
import Footer from "./footer";
import BrainwaveChart from "./BrainwaveChart";
import BrainwaveTest from "./BrainwaveTest";
import TrainBrainwaves from "./TrainBrainwaves";
import Link from "next/link"
export default function Home() {
  return (
    <div className="grid items-center justify-items-center gap-16 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center">
        <BrainwaveChart />
        <div className="flex flex-row justify-center gap-48">
          <div className="flex flex-col items-center justify-center">
              <h1 className="text-2xl font-bold mb-4">Brainwave Data Test</h1>
              <BrainwaveTest />
          </div>
          <div className="flex flex-col items-center justify-center">
              <h1 className="text-2xl font-bold mb-4">Train your Brainwaves</h1>
              <Link
                href="/train"
                className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-400"
            > Go to Training Center...
              </Link>  
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

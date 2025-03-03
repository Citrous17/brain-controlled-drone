"use client";
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

      
        {/* Three Buttons Below the Graph */}
        <div className="flex w-full justify-between mt-4">
          <button
            className="button button-primary flex-1 mx-2"
            onClick={() => alert("Train Model Clicked!")}
          >
            Train Model
          </button>
          <button
            className="button button-secondary flex-1 mx-2"
            onClick={() => alert("Reset Readings Clicked!")}
          >
            Reset Readings
          </button>
          <button
            className="button button-tertiary flex-1 mx-2"
            onClick={() => alert("Recalibrate Clicked!")}
          >
            Recalibrate
          </button>
        </div>

        <h2 className="text-xl font-semibold text-center sm:text-left mt-6">
          Drone Controls
        </h2>

        <div className="flex justify-center w-full">
          <button className="button button-primary self-start mx-2" onClick={() => alert("Move Forward Clicked!")}>
            Move Forward
          </button>
          <button className="button button-primary self-start mx-2" onClick={() => alert("Move Back Clicked!")}>
            Move Back
          </button>
          <button className="button button-primary self-start mx-2" onClick={() => alert("Move Up Clicked!")}>
            Move Up
          </button>
          <button className="button button-primary self-start mx-2" onClick={() => alert("Move Down Clicked!")}>
            Move Down
          </button>
          <button className="button button-primary self-start mx-2" onClick={() => alert("Move Left Clicked!")}>
            Move Left
          </button>
          <button className="button button-primary self-start mx-2" onClick={() => alert("Move Right Clicked!")}>
            Move Right
          </button>
        </div>
      </main>
      <Footer />
    </div>
  );
}

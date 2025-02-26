import Link from 'next/link'
import { BeakerIcon } from '@heroicons/react/24/solid'

export default function footer() {
    return (
        <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <Link href="/readme">
            <div className="flex gap-2 items-center justify-center text-sm">
            <BeakerIcon className="w-5 h-5" />
            <p className="text-sm">View Readme</p>  
            </div>
        </Link>
      </footer>
    )
}
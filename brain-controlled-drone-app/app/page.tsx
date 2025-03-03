import LandingPage from '@/app/ui/LandingPage';
import test from 'node:test';
import { testDb } from './lib/actions';

export default function Home() {
  testDb();
  return (
    <LandingPage />
  )
}

import LandingPage from '@/app/ui/LandingPage';
import test from 'node:test';
import { testDb, getData } from './lib/actions';

export default async function Home() {
  testDb();

  return (
    <LandingPage />
  )
}

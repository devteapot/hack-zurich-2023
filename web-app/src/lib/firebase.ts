import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
	apiKey: 'AIzaSyByBFm41NfIq7ZUMFa8UsVD1-F1V95tI2E',
	authDomain: 'hack-zurich-2023.firebaseapp.com',
	projectId: 'hack-zurich-2023',
	storageBucket: 'hack-zurich-2023.appspot.com',
	messagingSenderId: '293038517755',
	appId: '1:293038517755:web:8bffeb75c06bec006b2f5e'
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { app, db };

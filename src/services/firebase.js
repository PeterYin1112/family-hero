import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, onSnapshot, updateDoc, increment } from "firebase/firestore";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut, onAuthStateChanged } from "firebase/auth";

// 避免未安裝依賴時的錯誤
if (typeof window !== 'undefined' && !window.firebaseInitialized) {
  window.firebaseInitialized = false;
}

const firebaseConfig = {
  apiKey: "AIzaSyCagXSigdL09-OK4G5jF20Hj3iXnRVQs-M",
  authDomain: "family-hero-f89f7.firebaseapp.com",
  projectId: "family-hero-f89f7",
  storageBucket: "family-hero-f89f7.firebasestorage.app",
  messagingSenderId: "900050172486",
  appId: "1:900050172486:web:bdb1904fd5bc7cf9eba847",
  measurementId: "G-G3FBB69BBD"
};

let app = null;
let db = null;
let auth = null;
let provider = null;
let isInitialized = false;

export const initFirebase = () => {
  if (isInitialized) return true;
  
  try {
    app = initializeApp(firebaseConfig);
    db = getFirestore(app);
    auth = getAuth(app);
    provider = new GoogleAuthProvider();
    isInitialized = true;
    console.log("🔥 Firebase Initialized");
    return true;
  } catch (error) {
    console.error("Firebase initialization error:", error);
    return false;
  }
};

export const getFirestoreInstance = () => {
  if (!isInitialized) initFirebase();
  return db;
};

export const getAuthInstance = () => {
  if (!isInitialized) initFirebase();
  return auth;
};

export const getProviderInstance = () => {
  if (!isInitialized) initFirebase();
  return provider;
};

export const firebaseAuth = {
  signIn: async () => {
    try {
      const authInstance = getAuthInstance();
      const providerInstance = getProviderInstance();
      if (!authInstance || !providerInstance) throw new Error("Firebase not initialized");
      const result = await signInWithPopup(authInstance, providerInstance);
      return result.user;
    } catch (error) {
      console.error("Sign in error:", error);
      throw error;
    }
  },
  
  signOut: async () => {
    try {
      const authInstance = getAuthInstance();
      if (!authInstance) throw new Error("Firebase not initialized");
      await signOut(authInstance);
    } catch (error) {
      console.error("Sign out error:", error);
      throw error;
    }
  },
  
  onAuthStateChanged: (callback) => {
    const authInstance = getAuthInstance();
    if (!authInstance) return () => {};
    return onAuthStateChanged(authInstance, callback);
  }
};

export const firestoreService = {
  saveUserData: async (uid, data) => {
    try {
      const dbInstance = getFirestoreInstance();
      if (!dbInstance) throw new Error("Firestore not initialized");
      await setDoc(doc(dbInstance, "users", uid), data);
      return true;
    } catch (error) {
      console.error("Save error:", error);
      return false;
    }
  },
  
  loadUserData: async (uid) => {
    try {
      const dbInstance = getFirestoreInstance();
      if (!dbInstance) throw new Error("Firestore not initialized");
      const docRef = doc(dbInstance, "users", uid);
      const docSnap = await getDoc(docRef);
      if (docSnap.exists()) {
        return docSnap.data();
      }
      return null;
    } catch (error) {
      console.error("Load error:", error);
      return null;
    }
  },
  
  subscribeUserData: (uid, callback) => {
    try {
      const dbInstance = getFirestoreInstance();
      if (!dbInstance) return () => {};
      const docRef = doc(dbInstance, "users", uid);
      return onSnapshot(docRef, (docSnap) => {
        if (docSnap.exists()) {
          callback(docSnap.data());
        }
      });
    } catch (error) {
      console.error("Subscribe error:", error);
      return () => {};
    }
  },
  
  updateField: async (uid, field, value) => {
    try {
      const dbInstance = getFirestoreInstance();
      if (!dbInstance) throw new Error("Firestore not initialized");
      const docRef = doc(dbInstance, "users", uid);
      if (typeof value === 'number') {
        await updateDoc(docRef, { [field]: increment(value) });
      } else {
        await updateDoc(docRef, { [field]: value });
      }
      return true;
    } catch (error) {
      console.error("Update error:", error);
      return false;
    }
  }
};

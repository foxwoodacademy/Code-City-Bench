import React, { createContext, useReducer, useContext, useEffect } from 'react'
import type { AppState as AS } from '../types'

export type AppState = AS & { permissions: AS['permissions'] }

const initialState: AppState = {
  conversation: [],
  errorLog: [],
  simpleMode: true,
  permissions: { camera: undefined, microphone: undefined },
  apiKey: null,
}

type Action =
  | { type: 'ADD_MESSAGE'; payload: AppState['conversation'][0] }
  | { type: 'SET_API_KEY'; payload: string | null }
  | { type: 'TOGGLE_SIMPLE_MODE'; payload?: boolean }
  | { type: 'LOG_ERROR'; payload: AppState['errorLog'][0] }
  | { type: 'SET_PERMISSIONS'; payload: AppState['permissions'] }
  | { type: 'REHYDRATE'; payload: Partial<AppState> }
  | { type: 'CLEAR_CONVERSATION' }

function reducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'ADD_MESSAGE': {
      const nextConv = [...state.conversation, action.payload];
      // persist only last 20 turns
      const capped = nextConv.slice(-20);
      return { ...state, conversation: capped };
    }
    case 'SET_API_KEY':
      return { ...state, apiKey: action.payload }
    case 'TOGGLE_SIMPLE_MODE':
      return { ...state, simpleMode: action.payload ?? !state.simpleMode }
    case 'LOG_ERROR':
      return { ...state, errorLog: [...state.errorLog, action.payload] }
    case 'SET_PERMISSIONS':
      return { ...state, permissions: action.payload }
    case 'REHYDRATE':
      return { ...state, ...action.payload }
    case 'CLEAR_CONVERSATION':
      return { ...state, conversation: [] }
    default:
      return state
  }
}

const AppContext = createContext<{ state: AppState; dispatch: React.Dispatch<Action> }>({ state: initialState, dispatch: () => null })

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState)

  useEffect(() => {
    const payload = {
      conversation: state.conversation.slice(-20),
      simpleMode: state.simpleMode,
      apiKey: state.apiKey,
    }
    try { localStorage.setItem('captcoder_app_state_v1', JSON.stringify(payload)) } catch(e){}
  }, [state.conversation, state.simpleMode, state.apiKey])

  useEffect(() => {
    try {
      const raw = localStorage.getItem('captcoder_app_state_v1')
      if (raw) {
        const parsed = JSON.parse(raw)
        dispatch({ type: 'REHYDRATE', payload: parsed })
      }
    } catch (e) {
      console.warn('rehydrate failed', e)
    }
  }, [])

  return <AppContext.Provider value={{ state, dispatch }}>{children}</AppContext.Provider>
}

export const useAppContext = () => useContext(AppContext)

export interface Client {
  id: number
  cid: string
  ua: string
  createdAt: string
}

export interface Location {
  timestamp: number
  latitude: number
  longitude: number
  distance: number | null
  address: string
  clientId: number
  createdAt: string
}

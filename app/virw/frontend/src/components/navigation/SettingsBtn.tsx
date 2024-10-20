import { Settings } from "lucide-react";
import { Link } from "react-router-dom"
import AuthContext from "context/AuthContext";
import { useContext } from "react";
  

export default function SettingsBtn({}) {
    const { user } = useContext(AuthContext)
    if (!user?.is_staff) return null

    return (
        <a href={'/admin/'}>
            <Settings size={25} />
        </a>
    )
} 
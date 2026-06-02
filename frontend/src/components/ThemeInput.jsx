import {useState} from "react"

function ThemeInput({onSubmit}) {
    const [theme, setTheme]= useState("");
    const [error, setError] = useState("")
    const suggestions = ["Forest", "Space", "Ocean", "Castle", "Pirate", "Magic", "Garden", "Rainforest"]

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!theme.trim()) {
            setError("Please enter a theme name");
            return
        }

        onSubmit(theme.trim());
    }

    return <div className="theme-input-container">
        <h2>Generate Your Story</h2>
        <p>Enter a theme for your interactive story</p>

        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input
                    type="text"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    placeholder="Enter a theme (e.g. pirates, space, medieval...)"
                    className={error ? 'error' : ''}
                />
                {error && <p className="error-text">{error}</p>}
            </div>
            <div className="theme-suggestions">
                <p>Try one of these themes:</p>
                <div className="suggestion-list">
                    {suggestions.map((suggestion) => (
                        <button
                            key={suggestion}
                            type="button"
                            onClick={() => setTheme(suggestion)}
                            className="suggestion-btn"
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            </div>
            <button type="submit" className='generate-btn'>
                Generate Story
            </button>
        </form>
    </div>
}

export default ThemeInput;
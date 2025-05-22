import React, { useState, useRef, useEffect } from 'react';
import { 
  TextField, 
  IconButton, 
  Typography, 
  Box,
  useMediaQuery
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

// Create a theme with the colors from Figma
const theme = createTheme({
  palette: {
    primary: {
      main: '#49E883', // Green from the design
    },
    secondary: {
      main: '#434242', // Dark gray from the design
    },
    background: {
      default: '#000000', // Black background
      paper: '#1E1E1E', // Dark gray for elements
    },
    text: {
      primary: '#49E883', // Green text
      secondary: '#FFFFFF', // White text
    }
  },
  typography: {
    fontFamily: '"Jura", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 16,
          },
        },
      },
    },
  },
});

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const isMobile = useMediaQuery('(max-width:600px)');
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Format the messages as the API expects
      const apiMessages = [...messages, userMessage];
      
      const response = await axios.post('/api/chat', {
        messages: apiMessages,
      });
      
      const assistantMessage = { 
        role: 'assistant', 
        content: response.data.response,
        sources: response.data.sources
      };
      
      setMessages([...messages, userMessage, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, there was an error processing your request. Please try again later.'
      };
      setMessages([...messages, userMessage, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Inline SVG components for send button
  const SendIconInactive = () => (
    <svg width="31" height="30" viewBox="0 0 31 30" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M15.5 0.5C23.7999 0.5 30.5 7.0072 30.5 15C30.5 22.9928 23.7999 29.5 15.5 29.5C7.20015 29.5 0.5 22.9928 0.5 15C0.5 7.0072 7.20015 0.5 15.5 0.5Z" fill="#1E1E1E" stroke="#49E883"/>
      <path d="M15.5 7.5C15.5529 7.5 15.5993 7.51915 15.6299 7.54688V7.54785L24.4678 15.9141C24.4841 15.9295 24.5 15.9589 24.5 16C24.5 16.0206 24.4962 16.0384 24.4902 16.0527L24.4678 16.0859C24.424 16.127 24.3323 16.1368 24.2646 16.1162L24.208 16.0859L16.5127 8.80078L15.6689 8.00293V24.3662C15.6689 24.3852 15.6608 24.4172 15.627 24.4492C15.5931 24.4812 15.547 24.5 15.5 24.5C15.453 24.5 15.4069 24.4812 15.373 24.4492C15.3392 24.4172 15.3311 24.3852 15.3311 24.3662V8.00293L14.4873 8.80078L6.79199 16.0859C6.7721 16.1047 6.75385 16.1155 6.73633 16.1221C6.71768 16.129 6.69312 16.1338 6.66211 16.1338C6.6314 16.1338 6.60743 16.1289 6.58887 16.1221C6.57126 16.1155 6.55223 16.1048 6.53223 16.0859C6.51593 16.0705 6.5 16.0411 6.5 16C6.50001 15.9793 6.50376 15.9616 6.50977 15.9473L6.53223 15.9141L15.3701 7.54785L15.3691 7.54688C15.3997 7.51889 15.4468 7.5 15.5 7.5Z" fill="#49E883" stroke="#49E883"/>
    </svg>
  );

  const SendIconActive = () => (
    <svg width="31" height="30" viewBox="0 0 31 30" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M15.5 0.5C23.7999 0.5 30.5 7.0072 30.5 15C30.5 22.9928 23.7999 29.5 15.5 29.5C7.20015 29.5 0.5 22.9928 0.5 15C0.5 7.0072 7.20015 0.5 15.5 0.5Z" fill="#49E883" stroke="black"/>
      <path d="M15.974 7.18489C15.8479 7.06646 15.6776 7 15.5 7C15.3224 7 15.1521 7.06646 15.026 7.18489L6.18819 15.5514C5.93727 15.7889 5.93727 16.2112 6.18819 16.4487C6.32759 16.5807 6.49486 16.6335 6.66214 16.6335C6.82942 16.6335 6.9967 16.5807 7.1361 16.4487L14.8309 9.16434V24.3666C14.8309 24.7097 15.1376 25 15.5 25C15.8624 25 16.1691 24.7097 16.1691 24.3666V9.16434L23.8639 16.4487C24.1148 16.6863 24.5609 16.6863 24.8118 16.4487C25.0627 16.2112 25.0627 15.7889 24.8118 15.5514L15.974 7.18489Z" fill="black"/>
    </svg>
  );

  return (
    <ThemeProvider theme={theme}>
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          height: '100vh', 
          bgcolor: 'background.default',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Header wrapper for radius fix */}
        <Box
          sx={{
            width: '100%',
            bgcolor: 'secondary.main',
            borderBottomLeftRadius: '30px',
            borderBottomRightRadius: '30px',
            boxShadow: '0px 4px 4px 0px rgba(73,232,131,1.00)',
            overflow: 'hidden',
          }}
        >
          {/* Header content */}
          <Box 
            sx={{ 
              width: '100%', 
              height: '96px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              px: 3,
              position: 'relative',
              zIndex: 5,
            }}
          >
            <Typography
              variant="h6"
              sx={{
                fontFamily: '"Jura", sans-serif',
                fontWeight: 'bold',
                textAlign: 'center',
                color: '#49E883',
              }}
            >
              AJ's assistant
            </Typography>
          </Box>
        </Box>
        
        {/* Messages Container */}
        <Box 
          sx={{ 
            flexGrow: 1, 
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            p: 2,
            gap: 3,
          }}
        >
          {messages.length === 0 ? (
            <Box 
              sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center', 
                justifyContent: 'center',
                textAlign: 'center',
                height: '100%',
              }}
            >
              <Typography 
                variant="h5" 
                sx={{ 
                  fontFamily: '"Jura", sans-serif',
                  mb: 2,
                  color: 'primary.main'
                }}
              >
                Welcome to AJ's assistant
              </Typography>
              <Typography 
                variant="body1"
                sx={{ 
                  fontFamily: '"Jura", sans-serif',
                  color: 'primary.main'
                }}
              >
                I can assist you with information about Arun Jayesh's projects. For instance, if you need help understanding the codebase of his current projects or want to know more about a particular technology he's worked with, I'm here to help. Additionally, if you have any general questions about his work, feel free to ask!
              </Typography>
            </Box>
          ) : (
            <>
              {messages.map((message, index) => (
                <Box 
                  key={index} 
                  sx={{ 
                    display: 'flex',
                    flexDirection: 'column', 
                    alignItems: message.role === 'user' ? 'flex-end' : 'flex-start',
                    maxWidth: '100%'
                  }}
                >
                  {/* Sender Name */}
                  <Typography
                    sx={{
                      fontFamily: '"Jura", sans-serif',
                      fontWeight: 'bold',
                      mb: 1,
                      fontSize: '14px',
                      color: 'primary.main'
                    }}
                  >
                    {message.role === 'user' ? 'USER' : 'AJ\'S HELPER'}
                  </Typography>
                  
                  {/* Message Bubble */}
                  <Box
                    sx={{
                      maxWidth: '70%',
                      p: 2,
                      bgcolor: 'background.default',
                      border: '2px solid #49E883',
                      borderRadius: message.role === 'user' 
                        ? '30px 0 30px 30px' 
                        : '0 30px 30px 30px',
                      ...(message.role === 'user' ? { ml: 'auto' } : { mr: 'auto' }),
                    }}
                  >
                    <Typography 
                      sx={{ 
                        fontFamily: '"Jura", sans-serif',
                        color: 'primary.main'
                      }}
                    >
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </Typography>
                  </Box>
                </Box>
              ))}
              
              {/* Loading Indicator */}
              {isLoading && (
                <Box 
                  sx={{ 
                    display: 'flex',
                    flexDirection: 'column', 
                    alignItems: 'flex-start',
                    maxWidth: '100%'
                  }}
                >
                  <Typography
                    sx={{
                      fontFamily: '"Jura", sans-serif',
                      fontWeight: 'bold',
                      mb: 1,
                      fontSize: '14px',
                      color: 'primary.main'
                    }}
                  >
                    AJ'S HELPER
                  </Typography>
                  <Box
                    sx={{
                      p: 2,
                      bgcolor: 'background.default',
                      border: '2px solid #49E883',
                      borderRadius: '0 30px 30px 30px',
                      display: 'flex',
                      gap: 1,
                      justifyContent: 'center',
                      alignItems: 'center',
                      width: 'fit-content'
                    }}
                  >
                    <Box sx={{ width: 8, height: 8, bgcolor: '#49E883', borderRadius: '50%' }} />
                    <Box sx={{ width: 8, height: 8, bgcolor: '#49E883', borderRadius: '50%' }} />
                    <Box sx={{ width: 8, height: 8, bgcolor: '#49E883', borderRadius: '50%' }} />
                  </Box>
                </Box>
              )}
            </>
          )}
          <div ref={messagesEndRef} />
        </Box>
        
        {/* Input Area */}
        <Box 
          sx={{ 
            p: 2, 
            display: 'flex', 
            alignItems: 'center',
            bgcolor: 'background.default',
          }}
        >
          <TextField
            fullWidth
            placeholder="TYPE HERE"
            variant="outlined"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            multiline
            maxRows={4}
            sx={{ 
              '& .MuiOutlinedInput-root': {
                borderRadius: 16,
                border: '2px solid #49E883',
                '& fieldset': {
                  borderWidth: 0,
                },
                '&:hover fieldset': {
                  borderWidth: 0,
                },
                '&.Mui-focused fieldset': {
                  borderWidth: 0,
                },
              },
              '& .MuiInputBase-input': {
                fontFamily: '"Jura", sans-serif',
                color: '#49E883',
              },
              '& .MuiInputBase-input::placeholder': {
                color: '#49E883',
                opacity: 1,
              }
            }}
          />
          
          <IconButton 
            onClick={handleSend} 
            disabled={isLoading || !input.trim()}
            sx={{
              width: 32,
              height: 32,
              bgcolor: 'background.default',
              ml: 1,
              p: 0,
              '&:hover': {
                bgcolor: '#1E1E1E',
              },
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {input.trim() ? <SendIconActive /> : <SendIconInactive />}
          </IconButton>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App; 
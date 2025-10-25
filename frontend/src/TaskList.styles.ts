import React from 'react';


const isMobile = () => window.innerWidth <= 768;
const isTablet = () => window.innerWidth > 768 && window.innerWidth <= 1024;

export const getTaskListStyles = (loading: boolean) => {
  const mobile = isMobile();
  const tablet = isTablet();

  return {
    container: {
      display: 'flex',
      flexDirection: mobile ? ('column' as const) : ('row' as const),
      minHeight: '100vh',
      height: mobile ? 'auto' : '100vh',
      width: '100%',
      maxWidth: mobile ? '100%' : '1600px',
      margin: '0 auto',
      padding: mobile ? '0' : tablet ? '0 16px' : '0 24px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      overflow: mobile ? 'auto' : 'hidden',
      backgroundColor: '#f5f7fa',
      boxSizing: 'border-box' as const
    } as React.CSSProperties,

    leftPanel: {
      width: mobile ? '100%' : tablet ? '350px' : '400px',
      minWidth: mobile ? '100%' : tablet ? '350px' : '400px',
      padding: mobile ? '20px 16px' : '32px',
      backgroundColor: '#ffffff',
      borderRight: mobile ? 'none' : '1px solid #e1e8ed',
      borderBottom: mobile ? '1px solid #e1e8ed' : 'none',
      display: 'flex',
      flexDirection: 'column' as const,
      overflowY: mobile ? 'visible' : ('auto' as const),
      boxShadow: mobile ? '0 2px 4px rgba(0,0,0,0.04)' : '2px 0 8px rgba(0,0,0,0.04)',
      maxHeight: mobile ? 'none' : '100vh',
      flexShrink: 0
    } as React.CSSProperties,

    rightPanel: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column' as const,
      overflow: 'hidden',
      backgroundColor: '#f5f7fa',
      minWidth: 0,
      height: mobile ? 'auto' : '100vh',
      minHeight: mobile ? '50vh' : 'auto'
    } as React.CSSProperties,

    header: {
      padding: mobile ? '20px 16px 16px 16px' : tablet ? '24px 24px 20px 24px' : '32px 32px 24px 32px',
      backgroundColor: '#ffffff',
      borderBottom: '1px solid #e1e8ed'
    } as React.CSSProperties,

    taskListContainer: {
      flex: 1,
      overflowY: 'auto' as const,
      padding: mobile ? '16px' : tablet ? '20px 24px' : '24px 32px',
      boxSizing: 'border-box' as const
    } as React.CSSProperties,

    title: {
      fontSize: mobile ? '20px' : '24px',
      fontWeight: 600,
      color: '#1a1a1a',
      marginBottom: '8px'
    } as React.CSSProperties,

    subtitle: {
      fontSize: mobile ? '13px' : '14px',
      color: '#657786',
      marginBottom: mobile ? '16px' : '24px'
    } as React.CSSProperties,

    inputGroup: {
      marginBottom: mobile ? '16px' : '20px'
    } as React.CSSProperties,

    label: {
      display: 'block',
      fontSize: mobile ? '12px' : '13px',
      fontWeight: 600,
      color: '#14171a',
      marginBottom: '8px',
      textTransform: 'uppercase' as const,
      letterSpacing: '0.5px'
    } as React.CSSProperties,

    input: {
      width: '100%',
      padding: mobile ? '10px 14px' : '12px 16px',
      fontSize: mobile ? '14px' : '15px',
      border: '1px solid #e1e8ed',
      borderRadius: '8px',
      outline: 'none',
      transition: 'all 0.2s',
      backgroundColor: '#ffffff',
      color: '#14171a',
      boxSizing: 'border-box' as const
    } as React.CSSProperties,

    textarea: {
      width: '100%',
      padding: mobile ? '10px 14px' : '12px 16px',
      fontSize: mobile ? '14px' : '15px',
      border: '1px solid #e1e8ed',
      borderRadius: '8px',
      outline: 'none',
      resize: 'vertical' as const,
      fontFamily: 'inherit',
      transition: 'all 0.2s',
      minHeight: mobile ? '80px' : '100px',
      backgroundColor: '#ffffff',
      color: '#14171a',
      boxSizing: 'border-box' as const
    } as React.CSSProperties,

    addButton: {
      width: '100%',
      padding: mobile ? '12px' : '14px',
      fontSize: mobile ? '14px' : '15px',
      fontWeight: 600,
      color: 'white',
      backgroundColor: loading ? '#cbd5e0' : '#1da1f2',
      border: 'none',
      borderRadius: '8px',
      cursor: loading ? 'not-allowed' : 'pointer',
      transition: 'all 0.2s',
      marginBottom: mobile ? '16px' : '24px'
    } as React.CSSProperties,

    statsCard: {
      padding: mobile ? '16px' : '20px',
      backgroundColor: '#f7f9fc',
      borderRadius: '12px',
      border: '1px solid #e1e8ed'
    } as React.CSSProperties,

    statsTitle: {
      fontSize: mobile ? '11px' : '12px',
      fontWeight: 600,
      color: '#657786',
      marginBottom: '12px',
      textTransform: 'uppercase' as const,
      letterSpacing: '0.5px'
    } as React.CSSProperties,

    statItem: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: mobile ? '6px 0' : '8px 0',
      fontSize: mobile ? '13px' : '14px',
      color: '#14171a'
    } as React.CSSProperties,

    filterContainer: {
      display: 'flex',
      gap: mobile ? '8px' : '12px',
      marginTop: '16px',
      flexWrap: mobile ? ('wrap' as const) : ('nowrap' as const)
    } as React.CSSProperties,

    filterButton: (isActive: boolean) => ({
      padding: mobile ? '8px 14px' : '10px 20px',
      fontSize: mobile ? '13px' : '14px',
      fontWeight: 600,
      color: isActive ? '#1da1f2' : '#657786',
      backgroundColor: isActive ? '#e8f5fd' : 'transparent',
      border: 'none',
      borderRadius: '20px',
      cursor: 'pointer',
      transition: 'all 0.2s',
      whiteSpace: 'nowrap' as const
    } as React.CSSProperties),

    taskCard: (completed: boolean) => ({
      padding: mobile ? '16px' : '20px',
      backgroundColor: '#ffffff',
      border: '1px solid #e1e8ed',
      borderRadius: '12px',
      marginBottom: '12px',
      transition: 'all 0.2s',
      opacity: completed ? 0.7 : 1
    } as React.CSSProperties),

    taskHeader: {
      display: 'flex',
      flexDirection: mobile ? ('column' as const) : ('row' as const),
      justifyContent: 'space-between',
      alignItems: mobile ? 'stretch' : ('flex-start' as const),
      gap: mobile ? '12px' : '16px'
    } as React.CSSProperties,

    taskContent: {
      flex: 1
    } as React.CSSProperties,

    taskTitle: (completed: boolean) => ({
      fontSize: mobile ? '15px' : '16px',
      fontWeight: 600,
      color: completed ? '#657786' : '#14171a',
      marginBottom: '8px',
      textDecoration: completed ? 'line-through' : 'none',
      lineHeight: '1.4',
      wordBreak: 'break-word' as const
    } as React.CSSProperties),

    taskDescription: (completed: boolean) => ({
      fontSize: mobile ? '13px' : '14px',
      color: completed ? '#aab8c2' : '#657786',
      marginBottom: '8px',
      lineHeight: '1.5',
      wordBreak: 'break-word' as const
    } as React.CSSProperties),

    taskMeta: {
      fontSize: mobile ? '11px' : '12px',
      color: '#aab8c2'
    } as React.CSSProperties,

    actionButtons: {
      display: 'flex',
      gap: '8px',
      flexShrink: 0,
      flexDirection: mobile ? ('row' as const) : ('row' as const),
      justifyContent: mobile ? 'stretch' : ('flex-start' as const)
    } as React.CSSProperties,

    actionButton: (variant: 'complete' | 'delete' | 'undo') => ({
      padding: mobile ? '8px 12px' : '8px 16px',
      fontSize: mobile ? '12px' : '13px',
      fontWeight: 600,
      color: 'white',
      backgroundColor: variant === 'delete' ? '#e0245e' : variant === 'undo' ? '#ffad1f' : '#17bf63',
      border: 'none',
      borderRadius: '6px',
      cursor: 'pointer',
      transition: 'all 0.2s',
      whiteSpace: 'nowrap' as const,
      flex: mobile ? 1 : 'initial'
    } as React.CSSProperties),

    emptyState: {
      textAlign: 'center' as const,
      padding: mobile ? '60px 20px' : '80px 20px',
      color: '#aab8c2'
    } as React.CSSProperties,

    emptyIcon: {
      fontSize: mobile ? '40px' : '48px',
      marginBottom: '16px'
    } as React.CSSProperties,

    emptyText: {
      fontSize: mobile ? '14px' : '16px',
      color: '#657786'
    } as React.CSSProperties
  };
};


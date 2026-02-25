import request from 'supertest';
import { createApp } from '../../src/app';

describe('App base', () => {
  it('debería responder health check', async () => {
    const app = createApp();
    const res = await request(app).get('/health');

    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});
